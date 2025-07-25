<script lang="ts">
	import { tick } from 'svelte';

	// Form state
	let formData: {
		product_name: string;
		brand_name: string;
		category: string[];
		price: number | string;
		discounted_price: string;
		description: string;
		image_url: string;
		product_url: string;
		ad_type: string;
		ad_tone: string;
	} = {
		product_name: '',
		brand_name: '',
		category: [],
		price: '',
		discounted_price: '',
		description: '',
		image_url: '',
		product_url: '',
		ad_type: 'social_media',
		ad_tone: 'professional'
	};

	// UI state
	let isGenerating = $state(false);
	let generatedAd = $state('');
	let isStreaming = $state(false);
	let copySuccess = $state(false);
	let categoryInput = $state('');
	let responseExpanded = $state(true);
	let wordCount = $state(0);

	// Form validation
	let errors = $state<{
		product_name?: string;
		brand_name?: string;
		category?: string;
		price?: string;
		description?: string;
	}>({});

	const validateForm = () => {
		const newErrors: typeof errors = {};
		
		if (!formData.product_name.trim()) newErrors.product_name = 'Product name is required';
		if (!formData.brand_name.trim()) newErrors.brand_name = 'Brand name is required';
		if (formData.category.length === 0) newErrors.category = 'At least one category is required';
		if (!formData.price || Number(formData.price) <= 0) newErrors.price = 'Valid price is required';
		if (!formData.description.trim()) newErrors.description = 'Description is required';
		
		errors = newErrors;
		return Object.keys(newErrors).length === 0;
	};

	const addCategory = () => {
		const trimmedInput = categoryInput.trim();
		if (trimmedInput && !formData.category.includes(trimmedInput)) {
			formData.category = [...formData.category, trimmedInput];
			categoryInput = '';
		}
	};

	const removeCategory = (index: number) => {
		formData.category = formData.category.filter((_, i) => i !== index);
	}; 

	const handleCategoryKeydown = (event: KeyboardEvent) => {
		if (event.key === 'Enter') {
			event.preventDefault();
			addCategory();
		}
	};

	// Simulate streaming response
	const simulateStreaming = async (text: string) => {
		generatedAd = '';
		isStreaming = true;
		
		const words = text.split(' ');
		for (let i = 0; i < words.length; i++) {
			await new Promise(resolve => setTimeout(resolve, 50 + Math.random() * 100));
			generatedAd += (i > 0 ? ' ' : '') + words[i];
			
			// Auto-scroll to bottom of response area
			await tick();
			const responseArea = document.getElementById('response-area');
			if (responseArea) {
				responseArea.scrollTop = responseArea.scrollHeight;
			}
		}
		
		isStreaming = false;
		wordCount = generatedAd.trim().split(/\s+/).filter(word => word.length > 0).length;
	};

	const generateAd = async () => {
		if (!validateForm()) return;

		isGenerating = true;
		isStreaming = true;
		generatedAd = '';
		responseExpanded = true;

		try {
			const response = await fetch('http://127.0.0.1:8000/api/v1/generate-stream', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(formData)
			});

			if (!response.body) throw new Error('No response body');

			const reader = response.body.getReader();
			const decoder = new TextDecoder();
			let done = false;

			while (!done) {
				const { value, done: doneReading } = await reader.read();
				done = doneReading;
				if (value) {
					const chunk = decoder.decode(value);
					const lines = chunk.split('\n').filter(line => line.trim() !== '');
					for (const line of lines) {
						try {
							const parsed = JSON.parse(line);
							if (parsed.status === 'streaming' && parsed.content) {
								generatedAd += parsed.content;
								await tick();
								const responseArea = document.getElementById('response-area');
								if (responseArea) {
									responseArea.scrollTop = responseArea.scrollHeight;
								}
							}
						} catch (err) {
							console.error('Failed to parse streaming response:', err);
						}
					}
				}
			}
			wordCount = generatedAd.trim().split(/\s+/).filter(word => word.length > 0).length;
		} catch (err: unknown) {
			console.error('Streaming error:', err);
			generatedAd = '[ERROR] ' + (err instanceof Error ? err.message : 'Unknown error');
		} finally {
			isGenerating = false;
			isStreaming = false;
		}
	};

	const copyToClipboard = async () => {
		try {
			await navigator.clipboard.writeText(generatedAd);
			copySuccess = true;
			setTimeout(() => copySuccess = false, 2000);
		} catch (err) {
			console.error('Failed to copy text: ', err);
		}
	};

	const clearResponse = () => {
		generatedAd = '';
		responseExpanded = false;
		wordCount = 0;
	};
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
   <div class="container mx-auto px-2 py-2 max-w-10xl">
		<!-- Header Section -->
		<header class="text-center mb-12">
			<div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl mb-6 shadow-lg">
				<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
				</svg>
			</div>
			<h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-4">
				AI Ad Generator
			</h1>
			<p class="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
				Transform your product details into compelling, conversion-focused advertisements using the power of artificial intelligence
			</p>
		</header>

		<!-- Main Content -->
	   <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
		   <!-- Form Section -->
		   <div class="bg-white/80 backdrop-blur-md rounded-3xl p-10 shadow-2xl border border-white/30 flex flex-col justify-between lg:col-span-1 lg:min-h-[600px]">
				<h2 class="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
					<svg class="w-6 h-6 mr-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
					</svg>
					Product Details
				</h2>

				<form onsubmit={event => { event.preventDefault(); generateAd(); }} class="space-y-6">
					<!-- Product Name -->
					<div>
						<label for="product_name" class="block text-sm font-medium text-gray-700 mb-2">Product Name *</label>
						<input
							id="product_name"
							type="text"
							bind:value={formData.product_name}
							placeholder="e.g., Karlsburg Men's Solid Formal Shirt"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							class:border-red-300={errors.product_name}
						/>
						{#if errors.product_name}
							<p class="text-red-500 text-sm mt-1">{errors.product_name}</p>
						{/if}
					</div>

					<!-- Brand Name -->
					<div>
						<label for="brand_name" class="block text-sm font-medium text-gray-700 mb-2">Brand Name *</label>
						<input
							id="brand_name"
							type="text"
							bind:value={formData.brand_name}
							placeholder="e.g., Alice Bag"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							class:border-red-300={errors.brand_name}
						/>
						{#if errors.brand_name}
							<p class="text-red-500 text-sm mt-1">{errors.brand_name}</p>
						{/if}
					</div>

					<!-- Category -->
					<div>
						<label for="category" class="block text-sm font-medium text-gray-700 mb-2">Categories *</label>
						<div class="space-y-3">
							<div class="flex">
								<input
									id="category"
									type="text"
									bind:value={categoryInput}
									onkeydown={handleCategoryKeydown}
									placeholder="Add a category and press Enter"
									class="flex-1 px-4 py-3 rounded-l-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
								/>
								<button
									type="button"
									onclick={addCategory}
									class="px-4 py-3 bg-blue-500 text-white rounded-r-xl hover:bg-blue-600 transition-colors duration-200"
									aria-label="Add Category"
								>
									Add
								</button>
							</div>
							{#if formData.category.length > 0}
								<div class="flex flex-wrap gap-2">
									{#each formData.category as cat, index}
										<span class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
											{cat}
											<button
												type="button"
												onclick={() => removeCategory(index)}
												class="ml-2 text-blue-600 hover:text-blue-800"
												aria-label="Remove Category"
											>
												×
											</button>
										</span>
									{/each}
								</div>
							{/if}
						</div>
						{#if errors.category}
							<p class="text-red-500 text-sm mt-1">{errors.category}</p>
						{/if}
					</div>

					<!-- Price Fields -->
					<div class="grid md:grid-cols-2 gap-4">
						<div>
							<label for="price" class="block text-sm font-medium text-gray-700 mb-2">Price ($) *</label>
							<input
								id="price"
								type="number"
								step="0.01"
								min="0"
								bind:value={formData.price}
								placeholder="45.00"
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
								class:border-red-300={errors.price}
							/>
							{#if errors.price}
								<p class="text-red-500 text-sm mt-1">{errors.price}</p>
							{/if}
						</div>
						<div>
							<label for="discounted_price" class="block text-sm font-medium text-gray-700 mb-2">Sale Price ($)</label>
							<input
								id="discounted_price"
								type="number"
								step="0.01"
								min="0"
								bind:value={formData.discounted_price}
								placeholder="30.00"
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							/>
						</div>
					</div>

					<!-- Description -->
					<div>
						<label for="description" class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
						<textarea
							id="description"
							bind:value={formData.description}
							placeholder="Describe your product's key features and benefits..."
							rows="4"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 resize-none"
							class:border-red-300={errors.description}
						></textarea>
						{#if errors.description}
							<p class="text-red-500 text-sm mt-1">{errors.description}</p>
						{/if}
					</div>

					<!-- URLs -->
					<div class="space-y-4">
						<div>
							<label for="image_url" class="block text-sm font-medium text-gray-700 mb-2">Image URL</label>
							<input
								id="image_url"
								type="url"
								bind:value={formData.image_url}
								placeholder="https://example.com/product-image.jpg"
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							/>
						</div>
						<div>
							<label for="product_url" class="block text-sm font-medium text-gray-700 mb-2">Product URL</label>
							<input
								id="product_url"
								type="url"
								bind:value={formData.product_url}
								placeholder="https://example.com/product-page"
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							/>
						</div>
					</div>
 
					<!-- Configuration -->
					<div class="grid md:grid-cols-2 gap-4">
						<div>
							<label for="ad_type" class="block text-sm font-medium text-gray-700 mb-2">Ad Type</label>
							<select
								id="ad_type"
								bind:value={formData.ad_type}
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							>
								<option value="social_media">Social Media</option>
								<option value="email">Email</option>
								<option value="product_description">Product Description</option>
							</select>
						</div>
						<div>
							<label for="ad_tone" class="block text-sm font-medium text-gray-700 mb-2">Ad Tone</label>
							<select
								id="ad_tone"
								bind:value={formData.ad_tone}
								class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
							>
								<option value="professional">Professional</option>
								<option value="friendly">Friendly</option>
								<option value="urgent">Urgent</option>
								<option value="luxurious">Luxurious</option>
								<option value="playful">Playful</option>
								<option value="minimalist">Minimalist</option>
								<option value="bold">Bold</option>
								<option value="conversational">Conversational</option>
							</select>
						</div>
					</div>

					<!-- Generate Button -->
					<button
						type="submit"
						disabled={isGenerating}
						class="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold py-4 px-8 rounded-xl hover:from-blue-600 hover:to-indigo-700 focus:ring-4 focus:ring-blue-200 transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
						aria-label="Generate Ad"
					>
						{#if isGenerating}
							<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
							Generating...
						{:else}
							<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
							</svg>
							Generate Ad
						{/if}
					</button>
				</form>
			</div>

		   <!-- AI Response Section -->
		   <div class="bg-white/90 backdrop-blur-md rounded-3xl shadow-2xl border border-white/30 flex flex-col lg:col-span-1 lg:min-h-[50%] h-auto">
				<div class="p-6 border-b border-gray-100">
					<div class="flex items-center justify-between">
						<h2 class="text-2xl font-semibold text-gray-800 flex items-center">
							<svg class="w-6 h-6 mr-3 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 01-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
							</svg>
							Generated Ad
						</h2>
						<button
							onclick={() => responseExpanded = !responseExpanded}
							class="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
							aria-label="Toggle Response"
						>
							<svg class="w-5 h-5 transform transition-transform duration-200" class:rotate-180={!responseExpanded} fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
							</svg>
						</button>
					</div>
					{#if generatedAd}
						<div class="flex items-center justify-between mt-2">
							<p class="text-sm text-gray-500">{wordCount} words</p>
							<div class="flex space-x-2">
								<button
									onclick={copyToClipboard}
									class="inline-flex items-center px-3 py-1 text-sm bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors duration-200"
									class:bg-green-200={copySuccess}
									aria-label="Copy Ad"
								>
									{#if copySuccess}
										<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
										</svg>
										Copied!
									{:else}
										<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
										</svg>
										Copy
									{/if}
								</button>
								<button
									onclick={clearResponse}
									class="inline-flex items-center px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors duration-200"
									aria-label="Clear Response"
								>
									<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
									</svg>
									Clear
								</button>
							</div>
						</div>
					{/if}
				</div>
				{#if responseExpanded}
					<div class="flex-1 p-6">
						{#if !generatedAd && !isGenerating}
							<div class="flex flex-col items-center justify-center h-64 text-gray-400">
								<svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
								</svg>
								<p class="text-lg font-medium">Your AI-generated ad will appear here</p>
								<p class="text-sm">Fill out the form and click "Generate Ad" to get started</p>
							</div>
						{:else}
							<div
							   id="response-area"
							   class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6 min-h-[50vh] max-h-[50vh] overflow-y-auto"
							>
								{#if isGenerating && !generatedAd}
									<div class="flex items-center text-gray-500">
										<svg class="animate-spin -ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24">
											<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
											<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
										</svg>
										AI is crafting your perfect ad...
									</div>
								{:else if generatedAd}
									<div class="prose prose-gray max-w-none">
										<textarea
											class="whitespace-pre-wrap font-sans text-gray-800 leading-relaxed bg-transparent border border-gray-300 rounded-md p-2 w-full resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
											bind:value={generatedAd}
											style="width: 100%; height: 40vh;"
										></textarea>
										{#if isStreaming}
											<span class="inline-block w-2 h-5 bg-blue-500 animate-pulse ml-1"></span>
										{/if}
									</div>
								{/if}
							</div>
						{/if}
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>

<style>
	:global(body) {
		font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}
</style>
